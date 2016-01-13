FullMesh {
	description = "Full mesh within a single site"
	id="FullMesh_Local"

	host {
		id="h1"
		location="AMS"
		port {id="port11"}
		port {id="port12"}
		port {id="port13"}
		port {id="port14"}
	}

	host {
		id="h2"
		location="AMS"
		port {id="port21"}
		port {id="port22"}
		port {id="port23"}
		port {id="port24"}
	}

	host {
		id="h3"
		location="AMS"
		port {id="port31"}
		port {id="port32"}
		port {id="port33"}
		port {id="port34"}
	}

	host {
		id="h4"
		location="AMS"
		port {id="port41"}
		port {id="port42"}
		port {id="port43"}
		port {id="port44"}
	}

	host {
		id="h5"
		location="AMS"
		port {id="port51"}
		port {id="port52"}
		port {id="port53"}
		port {id="port54"}
	}

	link {
		id="l1"
		port {id="src"}
		port {id="dst"}
	}

	link {
		id="l2"
		port {id="src"}
		port {id="dst"}
	}

	link {
		id="l3"
		port {id="src"}
		port {id="dst"}
	}

	link {
		id="l4"
		port {id="src"}
		port {id="dst"}
	}

	link {
		id="l5"
		port {id="src"}
		port {id="dst"}
	}

	link {
		id="l6"
		port {id="src"}
		port {id="dst"}
	}

	link {
		id="l7"
		port {id="src"}
		port {id="dst"}
	}

	link {
		id="l8"
		port {id="src"}
		port {id="dst"}
	}

	link {
		id="l9"
		port {id="src"}
		port {id="dst"}
	}

	link {
		id="l10"
		port {id="src"}
		port {id="dst"}
	}

	adjacency h1.port14, l1.src
	adjacency h2.port24, l1.dst
	adjacency h1.port13, l6.src
	adjacency h3.port33, l6.dst
	adjacency h1.port12, l8.src
	adjacency h4.port42, l8.dst
	adjacency h1.port11, l5.src
	adjacency h5.port54, l5.dst
	adjacency h2.port23, l7.src
	adjacency h5.port53, l7.dst
	adjacency h2.port22, l9.src
	adjacency h4.port43, l9.dst
	adjacency h2.port21, l2.src
	adjacency h3.port34, l2.dst
	adjacency h3.port32, l10.src
	adjacency h5.port52, l10.dst
	adjacency h3.port31, l3.src
	adjacency h4.port44, l3.dst
	adjacency h4.port41, l4.src
	adjacency h5.port51, l4.dst

}


