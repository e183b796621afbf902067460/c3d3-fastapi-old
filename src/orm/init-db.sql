CREATE TABLE public.h_addresses (
	h_address_id serial4 NOT NULL,
	h_address text NOT NULL,
	h_address_load_ts timestamp NOT NULL DEFAULT now(),
	CONSTRAINT h_addresses_h_address_key UNIQUE (h_address),
	CONSTRAINT h_addresses_pkey PRIMARY KEY (h_address_id)
);

CREATE TABLE public.h_chains (
	h_chain_id serial4 NOT NULL,
	h_network_name text NOT NULL,
	h_network_id int4 NOT NULL,
	h_network_endpoint text NOT NULL,
	h_network_load_ts timestamp NOT NULL DEFAULT now(),
	CONSTRAINT h_chains_h_network_endpoint_key UNIQUE (h_network_endpoint),
	CONSTRAINT h_chains_h_network_id_key UNIQUE (h_network_id),
	CONSTRAINT h_chains_pkey PRIMARY KEY (h_chain_id)
);

CREATE TABLE public.h_protocols (
	h_protocol_id serial4 NOT NULL,
	h_protocol_name text NOT NULL,
	h_protocol_load_ts timestamp NOT NULL DEFAULT now(),
	CONSTRAINT h_protocols_pkey PRIMARY KEY (h_protocol_id)
);

CREATE TABLE public.h_protocols_categories (
	h_protocol_category_id serial4 NOT NULL,
	h_protocol_category_name text NOT NULL,
	h_network_load_ts timestamp NOT NULL DEFAULT now(),
	CONSTRAINT h_protocols_categories_pkey PRIMARY KEY (h_protocol_category_id)
);

CREATE TABLE public.h_labels (
	h_label_id serial4 NOT NULL,
	h_label_name text NOT NULL,
	h_label_password text NOT NULL,
	h_label_load_ts timestamp NOT NULL DEFAULT now(),
	CONSTRAINT h_labels_h_label_name_key UNIQUE (h_label_name),
	CONSTRAINT h_labels_pkey PRIMARY KEY (h_label_id)
);

CREATE TABLE public.l_addresses_chains (
	l_address_chain_id serial4 NOT NULL,
	h_address_id int4 NOT NULL,
	h_chain_id int4 NOT NULL,
	l_address_chain_name text NULL,
	CONSTRAINT l_addresses_chains_pkey PRIMARY KEY (l_address_chain_id),
	CONSTRAINT l_addresses_chains_h_address_id_fkey FOREIGN KEY (h_address_id) REFERENCES public.h_addresses(h_address_id),
	CONSTRAINT l_addresses_chains_h_chain_id_fkey FOREIGN KEY (h_chain_id) REFERENCES public.h_chains(h_chain_id)
);

CREATE TABLE public.l_protocols_categories (
	l_protocol_category_id serial4 NOT NULL,
	h_protocol_id int4 NOT NULL,
	h_protocol_category_id int4 NOT NULL,
	CONSTRAINT l_protocols_categories_pkey PRIMARY KEY (l_protocol_category_id),
	CONSTRAINT l_protocols_categories_h_protocol_category_id_fkey FOREIGN KEY (h_protocol_category_id) REFERENCES public.h_protocols_categories(h_protocol_category_id),
	CONSTRAINT l_protocols_categories_h_protocol_id_fkey FOREIGN KEY (h_protocol_id) REFERENCES public.h_protocols(h_protocol_id)
);

CREATE TABLE public.l_protocols_categories_chains (
	l_protocol_category_chain_id serial4 NOT NULL,
	l_protocol_category_id int4 NOT NULL,
	h_chain_id int4 NOT NULL,
	CONSTRAINT l_protocols_categories_chains_pkey PRIMARY KEY (l_protocol_category_chain_id),
	CONSTRAINT l_protocols_categories_chains_h_chain_id_fkey FOREIGN KEY (h_chain_id) REFERENCES public.h_chains(h_chain_id),
	CONSTRAINT l_protocols_categories_chains_l_protocol_category_id_fkey FOREIGN KEY (l_protocol_category_id) REFERENCES public.l_protocols_categories(l_protocol_category_id)
);

CREATE TABLE public.l_addresses_labels_chains (
	l_address_label_chain_id serial4 NOT NULL,
	l_address_chain_id int4 NOT NULL,
	h_label_id int4 NOT NULL,
	CONSTRAINT l_addresses_labels_chains_pkey PRIMARY KEY (l_address_label_chain_id),
	CONSTRAINT l_addresses_labels_chains_h_label_id_fkey FOREIGN KEY (h_label_id) REFERENCES public.h_labels(h_label_id),
	CONSTRAINT l_addresses_labels_chains_l_address_chain_id_fkey FOREIGN KEY (l_address_chain_id) REFERENCES public.l_addresses_chains(l_address_chain_id)
);

CREATE TABLE public.l_addresses_protocols_categories_chains (
	l_address_protocol_category_chain_id serial4 NOT NULL,
	l_protocol_category_chain_id int4 NOT NULL,
	l_address_chain_id int4 NOT NULL,
	l_address_label_chain_id int4 NOT NULL,
	CONSTRAINT l_addresses_protocols_categories_chains_pkey PRIMARY KEY (l_address_protocol_category_chain_id),
	CONSTRAINT l_addresses_protocols_categor_l_protocol_category_chain_id_fkey FOREIGN KEY (l_protocol_category_chain_id) REFERENCES public.l_protocols_categories_chains(l_protocol_category_chain_id),
	CONSTRAINT l_addresses_protocols_categories__l_address_label_chain_id_fkey FOREIGN KEY (l_address_label_chain_id) REFERENCES public.l_addresses_labels_chains(l_address_label_chain_id),
	CONSTRAINT l_addresses_protocols_categories_chains_l_address_chain_id_fkey FOREIGN KEY (l_address_chain_id) REFERENCES public.l_addresses_chains(l_address_chain_id)
);

CREATE TABLE public.s_addresses_protocols_categories_labels_chains (
	s_address_protocol_category_label_chain_id serial4 NOT NULL,
	l_address_protocol_category_chain_id int4 NOT NULL,
	CONSTRAINT s_addresses_protocols_categories_labels_chains_pkey PRIMARY KEY (s_address_protocol_category_label_chain_id),
	CONSTRAINT s_addresses_protocols_categor_l_address_protocol_category__fkey FOREIGN KEY (l_address_protocol_category_chain_id) REFERENCES public.l_addresses_protocols_categories_chains(l_address_protocol_category_chain_id) ON DELETE CASCADE
);
