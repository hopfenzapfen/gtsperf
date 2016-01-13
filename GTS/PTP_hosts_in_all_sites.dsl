PTP {
	description = "PTP"
	id="PTP_all_sites"

	host {
		id="h1ams"
		location="AMS"
		port {id="port11"}
	}

	host {
		id="h2ams"
		location="AMS"
		port {id="port21"}
	}

	link {
		id="l1ams"
		port {id="src"}
		port {id="dst"}
	}

	adjacency h1ams.port11, l1ams.src
	adjacency h2ams.port21, l1ams.dst

	host {
		id="h1prg"
		location="PRG"
		port {id="port12"}
	}

	host {
		id="h2prg"
		location="PRG"
		port {id="port22"}
	}

	link {
		id="l1prg"
		port {id="src"}
		port {id="dst"}
	}

	adjacency h1prg.port12, l1prg.src
	adjacency h2prg.port22, l1prg.dst

	host {
		id="h1mil"
		location="MIL"
		port {id="port13"}
	}

	host {
		id="h2mil"
		location="MIL"
		port {id="port23"}
	}

	link {
		id="l1mil"
		port {id="src"}
		port {id="dst"}
	}

	adjacency h1mil.port13, l1mil.src
	adjacency h2mil.port23, l1mil.dst

	host {
		id="h1bra"
		location="BRA"
		port {id="port14"}
	}

	host {
		id="h2bra"
		location="BRA"
		port {id="port24"}
	}

	link {
		id="l1bra"
		port {id="src"}
		port {id="dst"}
	}

	adjacency h1bra.port14, l1bra.src
	adjacency h2bra.port24, l1bra.dst

	host {
		id="h1lju"
		location="LJU"
		port {id="port15"}
	}

	host {
		id="h2lju"
		location="LJU"
		port {id="port25"}
	}

	link {
		id="l1lju"
		port {id="src"}
		port {id="dst"}
	}

	adjacency h1lju.port15, l1lju.src
	adjacency h2lju.port25, l1lju.dst
}


