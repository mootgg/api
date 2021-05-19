CREATE TABLE IF NOT EXISTS public.users (
    id                  BIGINT NOT NULL PRIMARY KEY,
    discord_id          BIGINT NOT NULL UNIQUE,
    username            VARCHAR(255) NOT NULL UNIQUE,
    avatar_hash         VARCHAR(255),
    bio                 TEXT DEFAULT NULL,
    banned              BOOLEAN NOT NULL DEFAULT FALSE,
    flags               BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS public.api_keys (
    token               VARCHAR(255) NOT NULL PRIMARY KEY,
    parent_id           BIGINT NOT NULL REFERENCES public.users (id) ON DELETE CASCADE,
    perms               BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS public.sessions (
    token               VARCHAR(255) NOT NULL PRIMARY KEY,
    parent_id           BIGINT NOT NULL REFERENCES public.users (id) ON DELETE CASCADE,
    expires             TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS public.moots (
    id                  BIGINT NOT NULL,
    author_id           BIGINT NOT NULL REFERENCES public.users (id) ON DELETE CASCADE,
    content             TEXT NOT NULL,
    hide                BOOLEAN NOT NULL DEFAULT FALSE,
    flags               BIGINT NOT NULL DEFAULT 0
);
