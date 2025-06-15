# /dev/video0
# /dev/video2

python -m lerobot.record \
    --robot.type=so101_follower \
    --robot.port=/dev/ttyACM1 \
    --robot.id=hackafollower \
    --robot.cameras="{ top: {type: opencv, index_or_path: 3, width: 640, height: 480, fps: 30}}" \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM0 \
    --teleop.id=hackaleader \
    --display_data=false \
    --dataset.repo_id=sovrasov/lecroc_gestures_1 \
    --dataset.reset_time_s=15 \
    --dataset.push_to_hub=false \
    --dataset.private=true \
    --dataset.num_episodes=10 \
    --dataset.single_task="Gestures" \
    --resume=True