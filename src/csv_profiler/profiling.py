
def is_missing(value: str | None) -> bool:
    if type(value) == str:
        value = value.strip()
        value = value.lower()
    
    
    if value == "" or value == "na" or value == "n/a" or value == "null" or value == "none" or value == "nan" or value ==  'none':
        return True
    else:
        return False
    

def try_float(value: str) -> float | None:
    """"Return Flot(value) or None if falis"""
    try:
        return float(value)
    except:
        return None
    


    
def infer_type(col : list) -> str:
        
    usable = []
    for item in col:
        if not is_missing(item):
            usable.append(item)
    if not usable:
        return("Text")
    for item in usable:
        if type(try_float(item)) is not float:
            if try_float(item) is None:
                return "Text"
    return "Number"
        
def column_Valuess(rows:list[dict[str,str]],col: str) -> list[str]:
    item=[]
    for row in rows:
        item.append(row.get(col,""))
    return(item)


def numeric_stats(values: list[str]) -> dict:
    """Compute stats for numeric column values (strings)."""
    numbers=[]
    miss=0
    for val in values:
        if is_missing(val):
           miss+=1
        else:
            n = try_float(val)
            if n is not None: 
                 numbers.append(n)
        
    return({f"count":len(numbers)," missing":miss, "unique":len(set(numbers)), "min":min(numbers), "max":max(numbers), "mean":sum(numbers)/len(numbers)})


def text_stats(values: list[str], top_k: int = 5) -> dict:
    
    missing=0
    usable=[]

    for val in values:
        if is_missing(val):
            missing+=1
        else:
            usable.append(val)

    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1
        top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    return{f"count":len(usable),"Missing":missing,"unique":len(set(usable)),"Top":top}


def basic_profile(rows: list[dict[str, str]]) -> dict:
    
    cols = list(rows[0].keys())

    report = {
        "source": None,  
        "summary": {
            "rows": len(rows),
            "columns": len(cols)
        },
        "columns": {}
    }

    for col in cols:
        
        values = column_Valuess(rows, col)

       
        col_type = infer_type(values)

       
        if col_type == "Number":
            stats = numeric_stats(values)
        else:
            stats = text_stats(values)

     
        report["columns"][col] = {
            "type": col_type.lower(),   
            "stats": stats
        }

    return report
 


def profile_rows(rows: list[dict[str, str]]) -> dict:
    
    col_profiles=[]
    cols = list(rows[0].keys())
    n_rows=len(rows)

    for col in cols:
        values = column_Valuess(rows,col)
        usable=[]
        missing=0

    

        for val in values:
            if is_missing(val):
                missing += 1
            else:
                usable.append(val)

        col_type = infer_type(values)

        profile = {
            "name": col,
            "type": col_type,
            "missing": missing,
            "missing_pct": 100.0 * missing / n_rows if n_rows else 0.0,
            "unique": len(set(usable)),
        }
        
        if col_type == "Number":
            nums = [try_float(v) for v in usable]
            nums = [x for x in nums if x is not None]
            if nums:
                profile.update({
                    "min": min(nums),
                    "max": max(nums),
                    "mean": sum(nums) / len(nums)
                })
        col_profiles.append(profile)




    return {"n_rows": n_rows, "n_cols": len(cols), "columns": col_profiles}



        
    
