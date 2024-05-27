script="scratch/scratch-simulator2"

nDevices=193

periods=(15 30 50 90 140 200)

for period in "${periods[@]}"; do
  folder="scratch/experiments/Test_${period}_${nDevices}/run"
  echo -n "Running experiments for period ${period}: "
  for r in `seq 1 30`; do
    echo -n " $r"
    mkdir -p ${folder}${r}
    ./ns3 run "$script --RngRun=$r --nDevices=$nDevices --period=${period}--OutputFolder=${folder}${r}" > "$folder${r}/log.txt" 2>&1
  done
  echo " END"
done

