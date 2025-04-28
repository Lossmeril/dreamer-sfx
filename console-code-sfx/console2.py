import asyncio
import random
import string
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.live import Live
from rich.text import Text

console = Console()

# Settings
MAX_CONSOLE_LINES = 70
CRITICAL_FAILURE_CHANCE = 0.008
SPECIAL_EVENT_CHANCE = 0.05

# Rich Progress Bar setup
progress = Progress(
    SpinnerColumn(),
    TextColumn("[bold cyan]{task.description}"),
    BarColumn(bar_width=30),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TimeElapsedColumn(),
    expand=True
)

console_lines = []
progress_bars = {}

async def generate_console_lines():
    verbs = ["CONNECTING", "LOADING", "AUTHENTICATING", "FETCHING", "SYNCHRONIZING", "TRANSMITTING", "BINDING", "INITIALIZING", "UPDATING", "DEPLOYING"]
    objects = ["MEMORY THREAD", "REMOTE CACHE", "ACCESS TOKEN", "CLUSTER NODE", "PACKET STREAM", "DATA SHARD", "SYSTEM REGISTRY", "SESSION KEYS"]
    modifiers = ["NODE", "PROCESS", "BUFFER", "SECTOR", "BRIDGE", "SEQUENCE", "VAULT", "SEGMENT"]
    statuses = ["OK", "FAIL", "TIMEOUT", "DENIED", "RETRY"]

    colors = {
        "OK": "green",
        "FAIL": "red",
        "TIMEOUT": "yellow",
        "DENIED": "red",
        "RETRY": "yellow"
    }

    while True:
        if random.random() < SPECIAL_EVENT_CHANCE:
            # Randomly insert a glitch or error
            if random.random() < 0.5:
                await insert_glitch_line()
            else:
                await insert_access_violation()
        else:
            verb = random.choice(verbs)
            obj = random.choice(objects)
            mod = random.choice(modifiers)
            number = random.randint(1000, 9999)
            status = random.choice(statuses)
            color = colors[status]

            if random.random() < 0.3:
                # Short line
                line = f"{verb} {mod} {number} [{color}]{status}[/{color}]"
            else:
                # Longer line
                line = f"{verb} {obj} VIA {mod} CHANNEL {number} - RESPONSE [{color}]{status}[/{color}]"
            
            console_lines.append(line)

        if len(console_lines) > MAX_CONSOLE_LINES:
            console_lines.pop(0)

        await asyncio.sleep(random.uniform(0.02, 0.07))

async def insert_glitch_line():
    glitched = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=random.randint(30, 70)))
    glitch_text = f"[bold red]!! GLITCH DETECTED: {glitched}[/bold red]"
    console_lines.append(glitch_text)
    if len(console_lines) > MAX_CONSOLE_LINES:
        console_lines.pop(0)

async def insert_access_violation():
    code = ''.join(random.choices("0123456789ABCDEF", k=8))
    error_text = f"[bold red]ACCESS VIOLATION - CODE 0x{code} - SYSTEM LOCKDOWN INITIATED[/bold red]"
    console_lines.append(error_text)
    if len(console_lines) > MAX_CONSOLE_LINES:
        console_lines.pop(0)

async def generate_hex_dumps():
    while True:
        await asyncio.sleep(random.uniform(3, 7))
        hex_line = ''.join(random.choices("0123456789ABCDEF", k=64))
        console_lines.append(f"[magenta]DUMP[/magenta] {hex_line}")
        if len(console_lines) > MAX_CONSOLE_LINES:
            console_lines.pop(0)

async def generate_progress_bars():
    task_counter = 1
    while True:
        await asyncio.sleep(random.uniform(1, 4))
        task_id = progress.add_task(f"INSTALL PKG-{task_counter}", total=100)
        progress_bars[task_counter] = task_id
        asyncio.create_task(update_progress_bar(task_counter))
        task_counter += 1

async def update_progress_bar(task_counter):
    task_id = progress_bars[task_counter]
    fail = random.random() < 0.2  # 20% chance to fail

    while not progress.finished:
        await asyncio.sleep(random.uniform(0.05, 0.15))
        if progress.tasks[task_id].finished:
            break
        progress.advance(task_id, random.randint(1, 6))

        if fail and progress.tasks[task_id].completed > random.randint(40, 85):
            progress.update(task_id, description=f"[red]FAILED PKG-{task_counter}[/red]")
            break

    await asyncio.sleep(1)
    progress.remove_task(task_id)
    del progress_bars[task_counter]

async def inject_critical_failures():
    while True:
        await asyncio.sleep(0.5)
        if random.random() < CRITICAL_FAILURE_CHANCE:
            console_lines.append("[bold red blink]CRITICAL SYSTEM FAILURE DETECTED! SYSTEM REBOOT REQUIRED![/bold red blink]")
            console_lines.append("[red]!!! STACK TRACE ABORTED // MEMORY CORE OFFLINE !!![/red]")
            if len(console_lines) > MAX_CONSOLE_LINES:
                console_lines.pop(0)

async def update_screen():
    progress.start()
    try:
        with Live(console=console, refresh_per_second=24, transient=False) as live:
            while True:
                table = Table.grid(expand=True)
                table.add_row(progress)
                table.add_row("")

                output = "\n".join(console_lines)
                panel = Panel(
                    Text.from_markup(output),
                    title="[bright_green]Console Output[/bright_green]",
                    border_style="green",
                    padding=(1, 2)
                )
                table.add_row(panel)

                live.update(table)
                await asyncio.sleep(0.04)
    finally:
        progress.stop()

async def main():
    await asyncio.gather(
        generate_console_lines(),
        generate_hex_dumps(),
        generate_progress_bars(),
        inject_critical_failures(),
        update_screen()
    )

if __name__ == "__main__":
    asyncio.run(main())
