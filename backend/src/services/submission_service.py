from datetime import datetime
from sys import stderr, stdout

from fastapi import HTTPException
from src.schemas import question_schemas
from src.commons.context import current_context
import asyncio
import aiofiles
import docker
from pathlib import Path
from src.models import question_model

client = docker.from_env()
async def submit(submission_req:question_schemas.SubmissionCreate):
    current_user = current_context.get().user
    ANSWER_FILE_NAME =  f"{current_user.username}{submission_req.question_id}{datetime.utcnow()}.txt"
    ANSWER_FILE_PATH = Path()/"submission"/"submission_answers"/ANSWER_FILE_NAME
    
    
    if submission_req.language == "python3":
        await eval_python3(submission_req,ANSWER_FILE_PATH)
    else:
        raise HTTPException(f"{submission_req.language} is not supported, yet.")
        
        
# async def prepare_submission(ANSWER_FILE_PATH):
#     answers = []
#     async with aiofiles.open(ANSWER_FILE_PATH, "r") as file:
#         answer =  question_model.Answer()
#         async for item in file:
# 	        if(item[:] == "tc_"):
#                 pass
#             pass
#         pass
            

async def eval_python3(submission_req:question_schemas.SubmissionCreate,ANSWER_FILE_PATH:str):
    cmd =  f"docker run -i --rm af26f0604926  /bin/sh"
   
    testcases = question_model.TestCase.get_by_attr("question_id")
    async with aiofiles.open(ANSWER_FILE_PATH, "wb+") as answer:
        proc = await asyncio.create_subprocess_shell(cmd, stdin=asyncio.subprocess.PIPE, stdout=answer, stderr=answer)
            
        for tc in testcases:
            try:
                await asyncio.wait_for(_eval_python3(submission_req.code,f"{tc.value}", testcase_id=tc.id, proc=proc),timeout=tc.timeout)
            except Exception as e:
                proc.stdin.write(b"TLE\n")
                await proc.stdin.drain()
            
            
        proc.stdin.write(b"exit\n")
        await proc.stdin.drain()
        await proc.wait()
        
    

async def _eval_python3(code:str,input_:str,testcase_id:int,proc:asyncio.subprocess.Process):
    proc.stdin.write(f"touch main.py && echo '{code}' > main.py && echo '{input_}' | python3 main.py\n".encode("utf-8"))
    await proc.stdin.drain()
    tc= "tc_"+str(testcase_id)
    proc.stdin.write(f"echo '{tc}'\n".encode("utf-8"))
    await proc.stdin.drain()
   


 

    
    
    

    