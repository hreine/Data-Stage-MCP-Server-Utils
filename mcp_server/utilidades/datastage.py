import subprocess
import json
from .config import datastage_config # Import the configuration
from .cache import get_from_cache, set_cache, generate_cache_key, init_cache_db # Import caching utilities

class DataStageError(Exception):
    """Custom exception for DataStage command errors."""
    pass

def _run_datastage_command(command_args):
    """Helper function to run DataStage commands."""
    try:
        result = subprocess.run(
            command_args,
            capture_output=True,
            text=True,
            check=False, # Raise an exception for non-zero exit codes
            encoding='utf-8'
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise DataStageError(
            f"DataStage command failed with exit code {e.returncode}:\n"
            f"Command: {' '.join(e.cmd)}\n"
            f"Stdout: {e.stdout.strip()}\n"
            f"Stderr: {e.stderr.strip()}"
        ) from e
    except FileNotFoundError:
        raise DataStageError(
            f"DataStage command not found. Ensure DataStage client is installed and in PATH. "\n"
            f"Attempted command: {' '.join(command_args)}"
        )

def dsjob_command(job_name: str, command: str, project: str = None, args: list = None) -> str:
    """
    Executes a dsjob command.

    Args:
        project: The DataStage project name. Defaults to DATASTAGE_PROJECT from config.
        job_name: The DataStage job name.
        command: The dsjob subcommand (e.g., 'run', 'log', 'status').
        args: Optional list of additional arguments for the dsjob subcommand.

    Returns:
        The stdout of the dsjob command.
    """
    if project is None:
        project = datastage_config.PROJECT

    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        f"-command",
        project,
        job_name
    ]
    if args:
        cmd.extend(args)
    return _run_datastage_command(cmd)

def export_job_to_file(object_name: str, output_file: str, project: str = None) -> str:
    """
    Exports a DataStage object.

    Args:
        project: The DataStage project name. Defaults to DATASTAGE_PROJECT from config.
        object_type: The type of object to export (e.g., 'JOB', 'TABLE').
        object_name: The name of the object to export.
        output_file: The path to the output file.

    Returns:
        A message indicating success or the stdout of the dsexport command.
    """
        
    cmd = [
        "dsexport",
        f"/D={datastage_config.DOMAIN}",
        f"/U={datastage_config.USER}",
        f"/P={datastage_config.PASSWORD}",
        f"/JOB={object_name}",
        r"/NODEPENDENTS",
        f"/D={datastage_config.SERVER}/{project}",
        f"{output_file}"
    ]
    _run_datastage_command(cmd) # dsexport usually doesn't return much to stdout on success
    return f"Successfully exported JOB {object_name} to {output_file}"

def dssearch_command(search_string: str, project: str = None, object_type: str = None) -> str:
    """
    Searches for DataStage objects.
    Note: dssearch is not a standard DataStage command-line tool.
    This function will simulate a search by listing jobs/components and filtering.
    A more robust solution would involve DataStage API or custom scripting.

    Args:
        project: The DataStage project name. Defaults to DATASTAGE_PROJECT from config.
        search_string: The string to search for.
        object_type: Optional type of object to search (e.g., 'JOB', 'TABLE').

    Returns:
        A JSON string of found objects.
    """
    if project is None:
        project = datastage_config.PROJECT

    cache_key = generate_cache_key(project, search_string, object_type)
    cached_result = get_from_cache(cache_key)
    if cached_result:
        return cached_result

    try:
        jobs_output = _run_datastage_command([
            "dsjob",
            "-domain", datastage_config.DOMAIN,
            "-server", datastage_config.SERVER,
            "-user", datastage_config.USER,
            "-password", datastage_config.PASSWORD,
            "-ljobs",
            project
        ])
        all_jobs = [job.strip() for job in jobs_output.split('\n') if job.strip()]

        found_objects = []
        for job in all_jobs:
            if search_string.lower() in job.lower():
                found_objects.append({"type": "JOB", "name": job})

        # If object_type is specified, filter further (though currently only JOBs are listed)
        if object_type:
            found_objects = [obj for obj in found_objects if obj["type"].lower() == object_type.lower()]

        result_json = json.dumps(found_objects, indent=2)
        set_cache(cache_key, result_json)
        return result_json

    except DataStageError as e:
        # If dsjob -ljobs fails, propagate the error
        raise e
    except Exception as e:
        raise DataStageError(f"An unexpected error occurred during dssearch simulation: {e}")

def get_datastage_domain() -> str:
    """
    Returns the configured DataStage domain.
    """
    return datastage_config.DOMAIN

def get_datastage_server() -> str:
    """
    Returns the configured DataStage server.
    """
    return datastage_config.SERVER

def get_projects() -> str:
    """
    Returns a list of available DataStage projects.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-lprojects"
    ]
    projects_output = _run_datastage_command(cmd)
    all_projects = [project.strip() for project in projects_output.split('\n') if project.strip()]
    print(all_projects)
    return json.dumps(all_projects)

def get_jobs(project: str = None) -> str:
    """
    Returns a list of jobs in a DataStage project.
    """

    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-ljobs",
        project
    ]
    jobs_output = _run_datastage_command(cmd)
    all_jobs = [job.strip() for job in jobs_output.split('\n') if job.strip()]
    return json.dumps(all_jobs)

def get_jobs_with_status(project: str, status: str) -> str:
    """
    Returns a list of jobs in a DataStage project with a specific status.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-ljobs",
        "-status", status,
        project
    ]
    jobs_output = _run_datastage_command(cmd)
    all_jobs = [job.strip() for job in jobs_output.split('\n') if job.strip()]
    return json.dumps(all_jobs)

def get_stages(project: str, job: str) -> str:
    """
    Returns a list of stages in a DataStage job.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-lstages",
        project,
        job
    ]
    stages_output = _run_datastage_command(cmd)
    all_stages = [stage.strip() for stage in stages_output.split('\n') if stage.strip()]
    return json.dumps(all_stages)

def get_links(project: str, job: str, stage: str) -> str:
    """
    Returns a list of links from a stage in a DataStage job.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-llinks",
        project,
        job,
        stage
    ]
    links_output = _run_datastage_command(cmd)
    all_links = [link.strip() for link in links_output.split('\n') if link.strip()]
    return json.dumps(all_links)

def get_params(project: str, job: str) -> str:
    """
    Returns a list of parameters for a DataStage job.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-lparams",
        project,
        job
    ]
    params_output = _run_datastage_command(cmd)
    all_params = [param.strip() for param in params_output.split('\n') if param.strip()]
    return json.dumps(all_params)

def get_invocations(project: str, job: str) -> str:
    """
    Returns a list of invocations for a DataStage job.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-linvocations",
        project,
        job
    ]
    invocations_output = _run_datastage_command(cmd)
    all_invocations = [invocation.strip() for invocation in invocations_output.split('\n') if invocation.strip()]
    return json.dumps(all_invocations)

def get_queues() -> str:
    """
    Returns a list of job queues.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-lqueues"
    ]
    queues_output = _run_datastage_command(cmd)
    all_queues = [queue.strip() for queue in queues_output.split('\n') if queue.strip()]
    return json.dumps(all_queues)

def get_job_info(project: str, job: str) -> str:
    """
    Returns information about a specific DataStage job.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-jobinfo",
        project,
        job
    ]
    job_info_output = _run_datastage_command(cmd)
    return job_info_output

def get_stage_info(project: str, job: str, stage: str) -> str:
    """
    Returns information about a specific DataStage stage.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-stageinfo",
        project,
        job,
        stage
    ]
    stage_info_output = _run_datastage_command(cmd)
    return stage_info_output

def get_link_info(project: str, job: str, stage: str, link: str) -> str:
    """
    Returns information about a specific DataStage link.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-linkinfo",
        project,
        job,
        stage,
        link
    ]
    link_info_output = _run_datastage_command(cmd)
    return link_info_output

def get_parameter_info(project: str, job: str, param: str) -> str:
    """
    Returns information about a specific DataStage parameter.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-paraminfo",
        project,
        job,
        param
    ]
    parameter_info_output = _run_datastage_command(cmd)
    return parameter_info_output

def get_log_job(project: str, job: str) -> str:
    """
    Returns log information for a specific DataStage job.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-logsum",
        project,
        job
    ]
    log_job_output = _run_datastage_command(cmd)
    return log_job_output

def get_report_job(project: str, job: str, report_type: str = "BASIC") -> str:
    """
    Genera un reporte para un job específico en un proyecto de DataStage.
    """
    cmd = [
        "dsjob",
        "-domain", datastage_config.DOMAIN,
        "-server", datastage_config.SERVER,
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-report",
        project,
        job,
        report_type
    ]
    report_output = _run_datastage_command(cmd)
    return report_output


def get_jobs_uses(project: str, job: str) -> str:
    """
    Returns log information for a specific DataStage job.
    """
    #dssearch.exe -domain datastage-was-qa.apps.ambientesbc.lab:9443 -user hreines -password 7BCB489E6C*2025 -server DATASTAGE-ENGINE-QA -ljobs -uses CERT_FIDUCIARIA JOB_TRF_CTA_INV_FON_P
    cmd = [
        "dssearch.exe",
        "-domain", datastage_config.DOMAIN,       
        "-user", datastage_config.USER,
        "-password", datastage_config.PASSWORD,
        "-server", datastage_config.SERVER,
        "-ljobs",
        "-uses",
        project,
        job
    ]
    log_job_output = _run_datastage_command(cmd)
    return log_job_output

