from asyncio.subprocess import PIPE
from fastapi import HTTPException
from src.schemas import question_schemas
from src.commons.context import current_context
import asyncio
import docker
from src.models import question_model

client = docker.from_env()


async def submit(submission_req: question_schemas.SubmissionCreate):
    current_user = current_context.get().user
    testcases = question_model.TestCase.get_by_attr(
        attr="question_id", value=submission_req.question_id)
    if submission_req.language == "python3":
        await eval_python3(submission_req, testcases=testcases)
    else:
        raise HTTPException(
            f"{submission_req.language} is not supported, yet.")


async def eval_python3(submission_req: question_schemas.SubmissionCreate, testcases):
    answers = []
    cmd = f"docker run -i --rm af26f0604926  /bin/sh"
    for tc in testcases:
        answer = question_model.Answer()
        answer.testcase_id = tc.id
        proc = await asyncio.create_subprocess_shell(cmd, stdin=asyncio.subprocess.PIPE, stdout=PIPE, stderr=PIPE)
        try:
            await asyncio.wait_for(_eval_python3(submission_req.code, f"{tc.value}", testcase_id=tc.id, proc=proc), timeout=tc.timeout)
        except Exception as e:
            answer.status = question_model.Status.time_limit_exceed
        ans, err = proc.communicate()
        exit_code = proc.returncode
        if exit_code == 0:
            if tc.ans == ans:
                answer.status = question_model.Status.accepted
            else:
                answer.status = question_model.Status.wrong_anwer
            answer.value = ans
        else:
            if answer.status is not None:
                answer.status = question_model.Status.runtime_error
            answer.value = err


async def _eval_python3(code: str, input_: str, testcase_id: int, proc: asyncio.subprocess.Process):
    proc.stdin.write(
        f"touch main.py && echo '{code}' > main.py && echo '{input_}' | python3 main.py\n".encode("utf-8"))
    await proc.stdin.drain()
