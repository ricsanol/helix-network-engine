from __future__ import annotations

from helix.core.settings import Settings
from helix.models.precheck_result import PreCheckResult
from helix.precheck.exceptions import PreCheckError
from helix.precheck.factory import create_precheck_components
from helix.precheck.logging.logger import setup_logger
from helix.precheck.serializers.precheck_report import save_precheck_report


class PreCheckEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.settings.ensure_directories()

        self.logger = setup_logger(
            name="helix.precheck",
            log_file=self.settings.logs_dir / "precheck.log",
            level=self.settings.log_level,
        )

    def run_for_service(self, service) -> PreCheckResult:
        """
        service deve ser um MobileServiceModel ou objeto compatível
        contendo ao menos:
        - hostname
        - vendor
        - modelo
        - loopback_ipv4
        - interface_serv
        - mobile_mgmt.vlan
        - mobile_control.vlan
        - mobile_data.vlan
        """

        host = service.loopback_ipv4
        modelo = getattr(service, "modelo", None)
        interface_name = service.interface_serv

        mgmt_vlan = getattr(service.mobile_mgmt, "vlan", None)
        control_vlan = getattr(service.mobile_control, "vlan", None)
        data_vlan = getattr(service.mobile_data, "vlan", None)

        reference_vlan = mgmt_vlan or control_vlan or data_vlan
        subinterface_name = (
            f"{interface_name}.{reference_vlan}" if reference_vlan else interface_name
        )

        vrf_name = None

        self.logger.info(
            "Iniciando pre-check | hostname=%s | vendor=%s | modelo=%s | host=%s | interface=%s | subinterface=%s | vrf=%s",
            service.hostname,
            service.vendor,
            modelo,
            host,
            interface_name,
            subinterface_name,
            vrf_name,
        )

        result = PreCheckResult(
            hostname=service.hostname,
            vendor=service.vendor,
            interface_name=interface_name,
            subinterface_name=subinterface_name,
            vrf_name=vrf_name,
        )

        try:
            if not host or str(host).strip() == "":
                raise PreCheckError(
                    f"Loopback /32 IPV4 não preenchido para o hostname {service.hostname}"
                )

            if not interface_name or str(interface_name).strip() == "":
                raise PreCheckError(
                    f"INTERFACE-SERV não preenchida para o hostname {service.hostname}"
                )

            client, validator = create_precheck_components(
                vendor=service.vendor,
                modelo=modelo,
                host=host,
                username=self.settings.ssh_username,
                password=self.settings.ssh_password,
                port=self.settings.ssh_port,
                timeout=self.settings.ssh_timeout,
                conn_timeout=self.settings.ssh_conn_timeout,
            )

            with client:
                result = validator.run(
                    hostname=service.hostname,
                    vendor=service.vendor,
                    interface_name=interface_name,
                    subinterface_name=subinterface_name,
                    vrf_name=vrf_name,
                )

            result.finalize()
            report_path = save_precheck_report(result, self.settings.reports_dir)
            result.report_path = str(report_path)

            self.logger.info(
                "Pre-check finalizado | hostname=%s | success=%s | report=%s",
                result.hostname,
                result.success,
                report_path,
            )

            return result

        except PreCheckError as exc:
            result.add_error(str(exc))
            result.finalize()

            report_path = save_precheck_report(result, self.settings.reports_dir)
            result.report_path = str(report_path)

            self.logger.error(
                "Falha controlada no pre-check | hostname=%s | erro=%s | report=%s",
                service.hostname,
                exc,
                report_path,
            )

            return result

        except Exception as exc:
            result.add_error(f"Erro inesperado: {exc}")
            result.finalize()

            report_path = save_precheck_report(result, self.settings.reports_dir)
            result.report_path = str(report_path)

            self.logger.exception(
                "Erro inesperado no pre-check | hostname=%s | report=%s",
                service.hostname,
                report_path,
            )

            return result