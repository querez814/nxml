
import subprocess
import os
import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from typing import Optional
from fastapi import Query

router = APIRouter()

@router.get("/latex")
async def latex_expression_to_png_bytes(
    expression: str = Query(..., max_length=1000),
    dpi: Optional[int] = Query(300, ge=72, le=600)
):
  
    start_time = time.time()
    
    if not expression:
        raise HTTPException(status_code=400, detail="Expression cannot be empty")
    
    temp_dir = f"temp_latex_{os.getpid()}_{int(time.time())}"
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        latex_doc = f"""
\\documentclass[preview,border=2pt]{{standalone}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}
\\begin{{document}}
${expression}$
\\end{{document}}
"""
        
        tex_file = os.path.join(temp_dir, "expression.tex")
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(latex_doc)
        
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", temp_dir, tex_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"LaTeX compilation failed: {result.stderr}")
        
        pdf_file = os.path.join(temp_dir, "expression.pdf")
        png_file = os.path.join(temp_dir, "expression.png")
        
        result = subprocess.run(
            [
                "convert",
                "-density", str(dpi),
                pdf_file,
                png_file
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Image conversion failed: {result.stderr}")
        
        with open(png_file, "rb") as f:
            png_data = f.read()
        
        duration = time.time() - start_time
        
        return Response(
            content=png_data,
            media_type="image/png",
            headers={
                "X-Process-Time": f"{duration:.4f}",
                "Content-Disposition": "inline; filename=expression.png"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing LaTeX: {str(e)}")
    
    finally:
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                try:
                    os.remove(os.path.join(temp_dir, file))
                except:
                    pass
            try:
                os.rmdir(temp_dir)
            except:
                pass