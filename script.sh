#!/bin/bash
while true
do
	printf "Options\n-------\n1. Weave\n2. Calico\n3. Flannel\n4. None\nSelect an overlay: "
	read character
	case $character in
	    1 ) echo "You selected 'Weave'."
		./Overlay/Weave/setup.sh "Press ENTER to bootstrap overlay."
	        ;;
	    2 ) echo "You selected 'Calico'."
		./Overlay/Calico/setup.sh "Press ENTER to bootstrap overlay."
	        ;;
	    3 ) echo "You selected 'Flannel'."
		./Overlay/Flannel/setup.sh "Press ENTER to bootstrap overlay."
     		;;
	    4)  echo "You selected not to install an overlay solution."
		break
		;;
	    * ) echo "You did not enter a number"
		clear
	esac
done
