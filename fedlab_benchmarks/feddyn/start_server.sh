#!/bin/bash
# ==========================================
# =============== EXPERIMENT ===============
# ==========================================
#ClientRankNum=10
#ClientNumPerRank=10
#ClientNum=$(($ClientNumPerRank * $ClientRankNum))
#WorldSize=$(($ClientRankNum + 1))
# balance iid cifar10 for 100 clients, check config.py for other setting
# python data_partition.py --out-dir ./Output/ --partition iid --balance True --dataset cifar10 --num-clients ${ClientNum} --seed 0
# echo -e "Data partition DONE.\n\n"
# sleep 4s

# # ----- FedAvg
# SECONDS=0

# python server_starter.py --world_size 11 --partition iid --alg FedAvg --out-dir ./Output/FedAvg/run1

# ELAPSED="Elapsed: $(($SECONDS / 3600))hrs $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"
# echo ELAPSED

# ------- FedDyn
#SECONDS=0
#
#python server_starter.py --world_size ${WorldSize} --partition iid --alg FedDyn --out-dir ./Output/FedDyn/run1
#
#ELAPSED="Elapsed: $(($SECONDS / 60))min $(($SECONDS % 60))sec"
#echo $ELAPSED



# ===========================================
# ================== DEBUG ==================
# ===========================================
ClientRankNum=3
ClientNumPerRank=10
ClientNum=$(($ClientNumPerRank * $ClientRankNum))
WorldSize=$(($ClientRankNum + 1))

# balance iid cifar10 for 30 clients, check config.py for other setting
python data_partition.py --out-dir ./Output/FedDyn/debug/ --partition iid --balance True --dataset cifar10 --num-clients ${ClientNum} --seed 0
echo -e "Data partition DONE.\n\n"
sleep 4s

# ------- FedDyn
SECONDS=0

python server_starter.py --debug --world_size ${WorldSize} --partition iid --alg FedDyn --out-dir ./Output/FedDyn/debug/

ELAPSED="Elapsed: $(($SECONDS / 60))min $(($SECONDS % 60))sec"
echo $ELAPSED
