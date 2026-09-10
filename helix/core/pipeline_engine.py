from __future__ import annotations

from helix.core.decision_engine import build_decision_reason, should_approve
from helix.models.pipeline_result import PipelineResult
from helix.templates.context_builder import build_cisco_context, build_huawei_context
from helix.templates.renderer import TemplateRenderer
from helix.templates.vendor_selector import get_template_and_builder


class PipelineEngine:
    def __init__(self, precheck_engine, output_orchestrator, logger) -> None:
        self.precheck_engine = precheck_engine
        self.output_orchestrator = output_orchestrator
        self.logger = logger
        self.renderer = TemplateRenderer()

    def run(self, service, cluster) -> PipelineResult:
        hostname = service.hostname
        vendor = service.vendor

        self.logger.info(
            "Iniciando pipeline | hostname=%s | vendor=%s",
            hostname,
            vendor,
        )

        # =========================
        # PRECHECK
        # =========================
        precheck_result = self.precheck_engine.run_for_service(
            service=service,
        )

        # =========================
        # DECISION
        # =========================
        approved = should_approve(precheck_result)
        decision_reason = build_decision_reason(precheck_result)

        self.logger.info(
            "Decisão | hostname=%s | approved=%s | motivo=%s",
            hostname,
            approved,
            decision_reason,
        )

        rendered_config = None

        # =========================
        # RENDER (apenas se aprovado)
        # =========================
        if approved:
            template_path, builder_type = get_template_and_builder(
                vendor=vendor,
                modelo=service.modelo,
            )

            if builder_type == "cisco":
                context = build_cisco_context(service, cluster)
            elif builder_type == "huawei":
                context = build_huawei_context(service, cluster)
            else:
                raise ValueError(f"Builder não suportado: {builder_type}")

            rendered_config = self.renderer.render(template_path, context)

            self.logger.info(
                "Render concluído | hostname=%s | template=%s",
                hostname,
                template_path,
            )

        else:
            self.logger.warning(
                "Render bloqueado | hostname=%s | motivo=%s",
                hostname,
                decision_reason,
            )

        # =========================
        # RESULT
        # =========================
        result = PipelineResult(
            hostname=hostname,
            vendor=vendor,
            approved=approved,
            decision_reason=decision_reason,
            precheck_result=precheck_result,
            rendered_config=rendered_config,
            report_path=getattr(precheck_result, "report_path", None),
        )

        # =========================
        # OUTPUT
        # =========================
        result = self.output_orchestrator.finalize(result)

        self.logger.info(
            "Pipeline finalizado | hostname=%s | status=%s | script=%s",
            hostname,
            result.status_label(),
            result.script_path,
        )

        return result