import time

import click
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn
from validations import validate_positive_int

validate_time_duration = validate_positive_int("duration cannot be less than 1 minute.")
validate_sessions = validate_positive_int("number of sessions cannot be less than 1")


@click.command()
@click.option(
    "-f",
    "--focus",
    type=int,
    default=25,
    show_default=True,
    help="Focus session duration in minutes",
    callback=validate_time_duration,
)
@click.option(
    "-s",
    "--short-break",
    type=int,
    default=5,
    show_default=True,
    help="Short break duration in minutes",
    callback=validate_time_duration,
)
@click.option(
    "-l",
    "--long-break",
    type=int,
    default=15,
    show_default=True,
    help="Long break duration in minutes",
    callback=validate_time_duration,
)
@click.option(
    "-s",
    "--sessions",
    type=int,
    default=4,
    show_default=True,
    help="Number of focus sessions before a long break",
    callback=validate_sessions,
)
@click.option(
    "-d",
    "--debug",
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
    help="Outputs debug logs",
)
def pommy(
    focus: int, short_break: int, long_break: int, sessions: int, debug: bool
) -> None:
    """
    Pommy is a dead-simple Pomodoro CLI.
    """

    progress = Progress(
        TextColumn("{task.description}", justify="right"),
        BarColumn(bar_width=None),
        TimeRemainingColumn(compact=True),
    )

    with progress:
        for session in range(sessions):
            current_session = f"{session + 1}/{sessions}"

            progress.add_task(
                description=f"[red]focus {current_session}",
                total=focus * 60,
                fields={"duration": focus * 60},
                visible=False,
            )

            if session + 1 == sessions:
                progress.add_task(
                    description=f"[blue]long ",
                    total=long_break * 60,
                    fields={"duration": long_break * 60},
                    visible=False,
                )
            else:
                progress.add_task(
                    description=f"[green]break {current_session}",
                    total=short_break * 60,
                    fields={"duration": short_break * 60},
                    visible=False,
                )

        for task in progress.tasks:
            task.visible = True

            for _ in range(task.fields["fields"]["duration"]):
                progress.advance(task.id, advance=1)
                time.sleep(1)

            task.visible = False
            task.completed = True


if __name__ == "__main__":
    pommy()
