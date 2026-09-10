from pathlib import Path

from helix.input.excel_reader import read_excel
from helix.input.mapper import map_row_to_service
from helix.input.cluster_reader import read_cluster_excel
from helix.input.cluster_mapper import map_row_to_cluster

from helix.core.cluster_resolver import find_cluster_by_hl3
from helix.core.precheck_engine import PreCheckEngine
from helix.core.pipeline_engine import PipelineEngine
from helix.core.output_orchestrator import OutputOrchestrator
from helix.core.settings import settings

from helix.precheck.logging.logger import setup_logger


def main() -> None:
    service_file = Path("data") / "helix_network_engine_template_mvp.xlsx"
    cluster_file = Path("data") / "helix_cluster_template.xlsx"
    output_dir = Path("outputs")
    log_file = output_dir / "logs" / "helix_pipeline.log"

    logger = setup_logger(
        name="helix_pipeline",
        log_file=log_file,
        level=settings.log_level,
    )

    logger.info("Iniciando Helix Network Engine")

    service_rows = read_excel(service_file)
    cluster_rows = read_cluster_excel(cluster_file)

    clusters = []
    for row in cluster_rows:
        if not row.get("HL3"):
            continue
        clusters.append(map_row_to_cluster(row))

    logger.info("Serviços carregados: %s", len(service_rows))
    logger.info("Clusters carregados: %s", len(clusters))

    precheck_engine = PreCheckEngine(settings=settings)
    output_orchestrator = OutputOrchestrator(settings=settings)
    pipeline_engine = PipelineEngine(
        precheck_engine=precheck_engine,
        output_orchestrator=output_orchestrator,
        logger=logger,
    )

    print("=== HELIX NETWORK ENGINE :: PIPELINE FINAL ===")
    print(f"Total services: {len(service_rows)}")
    print(f"Total clusters: {len(clusters)}")

    approved_count = 0
    blocked_count = 0
    error_count = 0

    for idx, row in enumerate(service_rows, start=4):
        try:
            if not row.get("Hostname"):
                logger.warning("Linha %s ignorada: Hostname vazio", idx)
                print(f"Linha {idx} ignorada: Hostname vazio")
                continue

            service = map_row_to_service(row)
            cluster = find_cluster_by_hl3(service.rr1, clusters)

            print("----------")
            print(f"Linha Excel: {idx}")
            print(f"Hostname: {service.hostname}")
            print(f"Vendor: {service.vendor}")
            print(f"Interface: {service.interface_serv}")
            print(f"RR1 / HL3 de busca: {service.rr1}")
            print(f"ID_SIGLA: {service.id_sigla}")

            logger.info(
                "Processando linha=%s hostname=%s vendor=%s rr1=%s",
                idx,
                service.hostname,
                service.vendor,
                service.rr1,
            )

            if not cluster:
                logger.warning(
                    "Cluster não encontrado para hostname=%s rr1=%s linha=%s",
                    service.hostname,
                    service.rr1,
                    idx,
                )
                print("Cluster não encontrado para este RR1/HL3")
                blocked_count += 1
                continue

            result = pipeline_engine.run(service=service, cluster=cluster)

            print(f"Status final: {result.status_label()}")
            print(f"Motivo: {result.decision_reason}")
            print(f"Report: {result.report_path}")

            if result.script_path:
                print(f"Script: {result.script_path}")

            if result.approved:
                approved_count += 1
                print("\n===== PREVIEW DO SCRIPT =====\n")
                print(result.rendered_config or "")
                print("\n============================\n")
            else:
                blocked_count += 1
                print("Render bloqueado pelo pre-check.\n")

        except Exception as exc:
            error_count += 1
            logger.exception("Erro na linha %s: %s", idx, exc)
            print(f"Erro na linha {idx}: {exc}")

    logger.info(
        "Execução finalizada | approved=%s blocked=%s errors=%s",
        approved_count,
        blocked_count,
        error_count,
    )

    print("=== RESUMO FINAL ===")
    print(f"Aprovados: {approved_count}")
    print(f"Bloqueados: {blocked_count}")
    print(f"Erros: {error_count}")


if __name__ == "__main__":
    main()