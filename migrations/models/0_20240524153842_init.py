from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "conversations" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL /* Primary Key */,
    "conversation_id" VARCHAR(255) NOT NULL UNIQUE /* Conversation id */,
    "avatar_slug" VARCHAR(255) NOT NULL  /* Avatar slug */,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* Creation timestamp */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* Last update timestamp */
);
CREATE TABLE IF NOT EXISTS "messages" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL /* Primary Key */,
    "persona_type" VARCHAR(5) NOT NULL  /* Type of persona */,
    "text" TEXT   /* text of message */,
    "media_url" VARCHAR(255)   /* media url or audio or video */,
    "visemes_url" VARCHAR(255)   /* visemes url from agent */,
    "word_timestamps_url" VARCHAR(255)   /* word timestamps url from agent */,
    "metadata" JSON   /* metadata for the message */,
    "media_type" VARCHAR(5)   /* type of media */,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* Creation timestamp */
);
CREATE TABLE IF NOT EXISTS "conversation_messages" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL /* Primary Key */,
    "order" INT NOT NULL  /* Order in which messages appear in the conversation */,
    "conversation_id" INT NOT NULL REFERENCES "conversations" ("id") ON DELETE CASCADE,
    "message_id" INT NOT NULL REFERENCES "messages" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "feedbacks" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "feedback_thumb" INT   /* thumbs up(true) or thumbs down(false) for the interaction */,
    "feedback_text" TEXT   /* detailed feedback on the interaction */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* Last update timestamp */,
    "message_id" INT NOT NULL REFERENCES "messages" ("id") ON DELETE CASCADE /* Message for which feedback is given */
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "webhooks" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "url" VARCHAR(255) NOT NULL,
    "headers" JSON,
    "method" VARCHAR(10) NOT NULL  DEFAULT 'POST',
    "get_text" INT NOT NULL  DEFAULT 1,
    "get_audio" INT NOT NULL  DEFAULT 0,
    "get_video" INT NOT NULL  DEFAULT 0,
    "video_width" INT NOT NULL  DEFAULT 320,
    "video_height" INT NOT NULL  DEFAULT 240,
    "video_frame_rate" INT NOT NULL  DEFAULT 25,
    "audio_bit_rate" INT NOT NULL  DEFAULT 32,
    "audio_sampling_rate" INT NOT NULL  DEFAULT 22050,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "avatars" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL /* Primary Key */,
    "name" VARCHAR(255) NOT NULL  /* Name for the avatar */,
    "slug" VARCHAR(255) NOT NULL UNIQUE /* Auto-generated unique identifier */,
    "provider" VARCHAR(6) NOT NULL  /* Provider for the avatar */,
    "settings" JSON NOT NULL  /* Settings for the avatar */,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* Creation timestamp */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* Last update timestamp */,
    "webhook_id" INT REFERENCES "webhooks" ("id") ON DELETE CASCADE /* Webhook to send the avatar to */
);
CREATE TABLE IF NOT EXISTS "records" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "key" VARCHAR(255) NOT NULL UNIQUE,
    "avatarId" VARCHAR(255) NOT NULL,
    "text" TEXT NOT NULL,
    "storage_paths" JSON NOT NULL,
    "created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "metadata" JSON
) /* A single cache record in the database */;
CREATE TABLE IF NOT EXISTS "usage_logs" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "timestamp" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "record_id" INT NOT NULL REFERENCES "records" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
