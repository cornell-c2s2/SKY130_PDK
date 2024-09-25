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
