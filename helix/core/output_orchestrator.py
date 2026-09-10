from __future__ import annotations

from pathlib import Path

from helix.core.settings import Settings
from helix.models.pipeline_result import PipelineResult


class OutputOrchestrator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def build_filename(self, hostname: str, vendor: str) -> str:
        hostname_norm = hostname.strip().lower().replace(" ", "_")
        vendor_norm = vendor.strip().lower().replace(" ", "_")
        return f"{hostname_norm}_{vendor_norm}"

    def save_rendered_config(
        self,
        hostname: str,
        vendor: str,
        rendered_config: str,
        approved: bool,
    ) -> Path:
        filename = self.build_filename(hostname, vendor)
        target_dir = self.settings.get_output_target_dir(approved)

        output_file = target_dir / f"{filename}.txt"

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(rendered_config, encoding="utf-8")

        return output_file

    def build_blocked_content(self, pipeline_result: PipelineResult) -> str:
        precheck_report_path = None
        if pipeline_result.precheck_result is not None:
            precheck_report_path = getattr(pipeline_result.precheck_result, "report_path", None)

        return (
            f"STATUS: blocked\n"
            f"HOSTNAME: {pipeline_result.hostname}\n"
            f"VENDOR: {pipeline_result.vendor}\n"
            f"MOTIVO: {pipeline_result.decision_reason}\n"
            f"REPORT: {precheck_report_path}\n"
        )

    def finalize(self, pipeline_result: PipelineResult) -> PipelineResult:
        """
        PreCheck já salvou o report.
        Aqui tratamos:
        - script aprovado
        - artefato de bloqueio
        """

        if pipeline_result.approved and pipeline_result.rendered_config:
            pipeline_result.script_path = self.save_rendered_config(
                hostname=pipeline_result.hostname,
                vendor=pipeline_result.vendor,
                rendered_config=pipeline_result.rendered_config,
                approved=True,
            )
            return pipeline_result

        blocked_content = self.build_blocked_content(pipeline_result)

        pipeline_result.script_path = self.save_rendered_config(
            hostname=pipeline_result.hostname,
            vendor=pipeline_result.vendor,
            rendered_config=blocked_content,
            approved=False,
        )

        return pipeline_result