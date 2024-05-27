script="scratch/scratch-simulator2"

nDevices=(1 20 70 120 193)

periods=25

for device in "${nDevices[@]}"; do
  folder="scratch/experiments/Test_${periods}_${device}/run"
  echo -n "Running experiments for device ${device}: "
  for r in `seq 1 30`; do
    echo -n " $r"
    mkdir -p ${folder}${r}
    ./ns3 run "$script --RngRun=$r --nDevices=$device --period=${periods}--OutputFolder=${folder}${r}" > "$folder${r}/log.txt" 2>&1
  done
  echo " END"
done

