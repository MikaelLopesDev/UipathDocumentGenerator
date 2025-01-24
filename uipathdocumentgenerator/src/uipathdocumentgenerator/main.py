import sys
import warnings
import os
import pandas as pd
from pathlib import Path

from uipathdocumentgenerator.crew import Uipathdocumantationgenerator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
current_project_path = Path.home() / "Downloads"

IGNORED_FOLDERS = [
    ".entities", ".objects", ".project", ".settings", ".templates", ".tmh", ".local",
    "Documentation", "Exceptions_Screenshots", "Tests"
]
IGNORED_FILES = ["LICENSE"]

def validate_directory(directory):
    """Validate if the given directory exists and is accessible."""
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"The path '{directory}' is not a directory.")

def run():
    """Run the crew."""
    try:
        # Solicita o diretório de entrada ao usuário
        input_directory = input("Enter the path to the input directory: ").strip()
        print(f"Input directory: {input_directory}")
        validate_directory(input_directory)

        # Cria a instância do crew
        crew_instance = Uipathdocumantationgenerator(
            input_directory=input_directory,
            ignored_folders=IGNORED_FOLDERS,
            ignored_files=IGNORED_FILES
        )

        print(f"Launching crew with directory: {input_directory}")
        crew_instance.crew().kickoff(inputs={
            "directory": input_directory,
            "ignored_folders": IGNORED_FOLDERS,
            "ignored_files": IGNORED_FILES,
            "DiretorioName": str(current_project_path)
        })
        print("Execution completed successfully.")

        # Checa se o atributo usage_metrics existe antes de acessá-lo
        if hasattr(crew_instance, 'usage_metrics') and crew_instance.usage_metrics is not None:
            costs = 0.150 * (
                crew_instance.usage_metrics.prompt_tokens +
                crew_instance.usage_metrics.completion_tokens
            ) / 1_000_000
            print(f"Total costs: ${costs:.4f}")

            # Converte UsageMetrics em DataFrame, se disponível
            df_usage_metrics = pd.DataFrame([crew_instance.usage_metrics.model_dump()])
            print(df_usage_metrics)
        else:
            print("Usage metrics não foram geradas.")

    except Exception as e:
        print(f"Error: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Uipathdocumantationgenerator().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Uipathdocumantationgenerator().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Uipathdocumantationgenerator().crew().test(
            n_iterations=int(sys.argv[1]),
            openai_model_name=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
