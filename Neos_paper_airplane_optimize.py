import optuna 
from fastapi import FastAPI
from starlette.websockets import WebSocket

app  = FastAPI()
study = optuna.create_study(study_name ="paper_airplane_optimize_17",storage='sqlite:///paper_airplane_optimize.db',load_if_exists=True,direction="maximize")

@app.get("/")
async def getAccess():
    return {"success"}

@app.get("/study/name")
async def getStudyName():
    return study.study_name
@app.get("/study/best_params")
async def getBestParams():
    return study.best_params
@app.get("/study/best_value")
async def getBestValue():
    return study.best_value
@app.get("/study/trial_count")
async def getTrialCount():
    return study.trials[-1]._trial_id
@app.websocket("/ws/paper_airplane_optimize/")
async def websocket_endpoint(ws:WebSocket,n_trial=10):
    await ws.accept()
    for step in range(int(n_trial)):
        trial = study.ask()
        theta_launch_pad = trial.suggest_float("theta_launch_pad",0,90)
        theta_main_wing = trial.suggest_float("theta_main_wing",-90,90)
        theta_sub_wing = trial.suggest_float("theta_sub_wing",-90,90)
        phi_main_wing = trial.suggest_float("phi_main_wing",-90,90)
        psi_tail_wing = trial.suggest_float("psi_tail_wing",-90,90)
        position_main_wing = trial.suggest_float("position_main_wing",0,1)
        position_sub_wing = trial.suggest_float("position_sub_wing",0,1)
        await ws.send_text(f"theta_launch_pad:{theta_launch_pad},theta_main_wing:{theta_main_wing},theta_sub_wing:{theta_sub_wing},phi_main_wing:{phi_main_wing},\
                           psi_tail_wing:{psi_tail_wing},position_main_wing:{position_main_wing},position_sub_wing:{position_sub_wing}")
        data = await ws.receive_text()
        study.tell(trial,data)