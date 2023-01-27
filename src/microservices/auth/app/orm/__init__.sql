CREATE TABLE public.h_sessions (
	h_session_id serial4 NOT NULL,
	h_session_name text NOT NULL,
	h_session_password text NOT NULL,
	h_session_load_ts timestamp NOT NULL DEFAULT now(),
	CONSTRAINT h_sessions_h_session_name_key UNIQUE (h_session_name),
	CONSTRAINT h_sessions_pkey PRIMARY KEY (h_session_id)
);