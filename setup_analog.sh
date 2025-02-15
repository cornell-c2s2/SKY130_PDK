#Cadence Virtuoso
module load cadence/cadence
module load cadence/innovus
#For parasitic extraction:
export ASSURAHOME=/opt/cadence/ASSURA41
export PATH=$ASSURAHOME/tools/bin:$PATH
export QRC_HOME=/opt/cadence/EXT152
export PATH=$QRC_HOME/bin:$QRC_HOME/tools/bin:$PATH
export PATH=/opt/cadence/SPECTRE231/bin:$PATH
export PATH=/opt/cadence/XCELIUM2403/tools.lnx86/bin/:$PATH
unset OA_HOME
#
export CDS_Netlisting_Mode=Analog
# SKY130 Specific Pegasus
export OA_HOME=~/SKY130_PDK/oa
export PEGASUS_DRC=~/SKY130_PDK/sky130_release/Sky130_DRC
export PEGASUS_LVS=~/SKY130_PDK/sky130_release/Sky130_LVS
