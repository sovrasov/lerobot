rm -rf /home/sovrasov/.cache/huggingface/lerobot/sovrasov/eval_red_ball_3
python -m lerobot.record  \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM1 \
  --robot.id=hackafollower \
  --robot.cameras="{ top: {type: opencv, index_or_path: 3, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 5, width: 640, height: 480, fps: 30}}" \
  --display_data=false \
  --dataset.repo_id=sovrasov/eval_red_ball_3 \
  --dataset.single_task="Put the red ball to the cup" \
  --policy.path=/home/sovrasov/.cache/huggingface/hub/models--kprokofi--lecroc_red_ball_3cams_50/snapshots/1b712a5e3e532e36e0eeb1a782e6d45842928004/pretrained_model/
  #--policy.path=/home/sovrasov/.cache/huggingface/hub/models--kprokofi--lecroc_red_ball_3cams_18/snapshots/7dd4ff52780c60732ad768b356f86c494d829702/pretrained_model/
  #--policy.path=/home/sovrasov/.cache/huggingface/hub/models--kprokofi--act_red_ball_1/snapshots/34d4e64c90fbefe8a19c37e044581cbf9ff9c903/pretrained_model/

  #--robot.cameras="{ wrist: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 3, width: 640, height: 480, fps: 30}, front: {type: intelrealsense, serial_number_or_name: 218622276417, width: 640, height: 480, fps: 30, color_mode: rgb, rotation: 0}}" \
  #--robot.cameras="{ wrist: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}, front: {type: intelrealsense, serial_number_or_name: 218622276417, width: 640, height: 480, fps: 30, color_mode: rgb, rotation: 0}}" \
  #--robot.cameras="{ wrist: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 3, width: 640, height: 480, fps: 30}}" \


  #--robot.cameras="{ wrist: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 3, width: 640, height: 480, fps: 30}, top: {type: opencv, index_or_path: 5, width: 640, height: 480, fps: 30}}" \
