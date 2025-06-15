import socket

from enum import Enum
import subprocess

class LaCrocCommands(Enum):
    talk = "<TALK>"
    stop = "<STOP>"
    yes = "<YES>"
    no = "<NO>"
    speak = "<SPEAK>"
    bring_ball = "<GET_BALL>"

    # 0: yes, 1:yes,  2: no, 3: talk, 4: talk, 5:jump
COMMAND_2_EPISODE = {
    LaCrocCommands.talk.value: 3,
    LaCrocCommands.yes.value: 1,
    LaCrocCommands.no.value: 2,
    LaCrocCommands.speak.value: 5,
    LaCrocCommands.bring_ball.value: -1,
}

import logging
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from pprint import pformat

import draccus

from lerobot.common.datasets.lerobot_dataset import LeRobotDataset
from lerobot.common.robots import (  # noqa: F401
    Robot,
    RobotConfig,
    koch_follower,
    make_robot_from_config,
    so100_follower,
    so101_follower,
)
from lerobot.common.utils.robot_utils import busy_wait
from lerobot.common.utils.utils import (
    init_logging,
    log_say,
)


@dataclass
class DatasetReplayConfig:
    # Dataset identifier. By convention it should match '{hf_username}/{dataset_name}' (e.g. `lerobot/test`).
    repo_id: str
    # Episode to replay.
    episode: int
    # Root directory where the dataset will be stored (e.g. 'dataset/path').
    root: str | Path | None = None
    # Limit the frames per second. By default, uses the policy fps.
    fps: int = 30


@dataclass
class ReplayConfig:
    robot: RobotConfig
    dataset: DatasetReplayConfig
    # Use vocal synthesis to read events.
    play_sounds: bool = True

@draccus.wrap()
def server_program(cfg: ReplayConfig):
    print("Running server")

    init_logging()
    logging.info(pformat(asdict(cfg)))

    robot = make_robot_from_config(cfg.robot)
    robot.connect()

    def run_inference():
        subprocess.run(["rm -rf /home/sovrasov/.cache/huggingface/lerobot/sovrasov/eval_red_ball_3"])
        args = ["--robot.type=so101_follower",
                "--robot.port=/dev/ttyACM1",
                "--robot.id=hackafollower",
                '--robot.cameras="{ top: {type: opencv, index_or_path: 3, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 5, width: 640, height: 480, fps: 30}}"',
                "--display_data=false",
                "--dataset.repo_id=sovrasov/eval_red_ball_3",
                '--dataset.single_task="Put the red ball to the cup"',
                '--policy.path=/home/sovrasov/.cache/huggingface/hub/models--kprokofi--lecroc_red_ball_3cams_50/snapshots/1b712a5e3e532e36e0eeb1a782e6d45842928004/pretrained_model/'
        ]
        subprocess.run(["python", "-m", "lerobot.record", args])

    def run_action(episode_idx: int):
        if episode_idx < 0:
            run_inference()
            return

        dataset = LeRobotDataset(cfg.dataset.repo_id, root=cfg.dataset.root, episodes=[episode_idx])
        actions = dataset.hf_dataset.select_columns("action")

        for idx in range(dataset.num_frames):
            start_episode_t = time.perf_counter()

            action_array = actions[idx]["action"]
            action = {}
            for i, name in enumerate(dataset.features["action"]["names"]):
                action[name] = action_array[i]

            robot.send_action(action)

            dt_s = time.perf_counter() - start_episode_t
            busy_wait(1 / dataset.fps - dt_s)


    # get the hostname
    host = ""
    port = 33333  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break

        print("from connected user: " + str(data))
        action_type = data.split(">")[0] + ">"
        action_idx = COMMAND_2_EPISODE[action_type]
        run_action(action_idx)

    conn.close()  # close the connection

    robot.disconnect()


if __name__ == '__main__':
    server_program()