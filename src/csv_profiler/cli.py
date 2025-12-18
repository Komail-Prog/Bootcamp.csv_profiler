import json
import typer
from pathlib import Path

from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown, write_json

def main(
    input_path: Path = typer.Argument(..., help="Path to the input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", "-o", help="Folder to save the reports"),
    report_name: str = typer.Option("report", "--report-name", "-n", help="Base name for the output files"),
    preview: bool = typer.Option(False, "--preview", help="Show a quick summary in the terminal"),
):
  
   
    out_dir.mkdir(parents=True, exist_ok=True)
    
  
    try:
        rows = read_csv_rows(input_path)
        report = profile_rows(rows)
        
       
        write_json(report, out_dir / f"{report_name}.json")
        
       
        md_content = render_markdown(report)
        md_path = out_dir / f"{report_name}.md"
        md_path.write_text(md_content, encoding="utf-8")
        
        typer.secho(f" Success! Reports saved to: {out_dir}", fg=typer.colors.GREEN, bold=True)

        if preview:
            typer.echo("--- Quick Summary ---")
            typer.echo(f"Rows: {report.get('n_rows')}")
            typer.echo(f"Columns: {report.get('n_cols')}")

    except Exception as e:
        typer.secho(f" Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    typer.run(main)