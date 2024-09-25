#Cadence Virtuoso
module load cadence/cadence
#For parasitic extraction:
export ASSURAHOME=/opt/cadence/assura
export PATH=$ASSURAHOME/tools/bin:$PATH
export QRC_HOME=/opt/cadence/EXT152
export PATH=$QRC_HOME/bin:$QRC_HOME/tools/bin:$PATH
unset OA_HOME
#
export CDS_Netlisting_Mode=Analog
# SKY130 Specific Pegasus
export OA_HOME=/opt/cadence/IC231/oa_v22.61.015
export PEGASUS_DRC=~/SKY130_PDK/sky130_release/Sky130_DRC
export PEGASUS_LVS=~/SKY130_PDK/sky130_release/Sky130_LVS
