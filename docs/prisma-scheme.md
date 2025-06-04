// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

enum ChatType {
  PRIVATE
  GROUP
  CHANNEL
  FORUM
}

enum MediaType {
  PHOTO
  VIDEO
  DOCUMENT
  AUDIO
  VOICE
  STICKER
  OTHER
}

enum DownloadStatus {
  SUCCESS
  ERROR
}

model User {
  id          Int      @id @default(autoincrement())
  telegramId  BigInt   @unique
  username    String?  @db.VarChar(64)
  firstName   String?  @db.VarChar(128)
  lastName    String?  @db.VarChar(128)
  sessions    Session[]
  chats       Chat[]
  createdAt   DateTime @default(now())
}

model Session {
  id            Int      @id @default(autoincrement())
  user          User     @relation(fields: [userId], references: [id])
  userId        Int
  authKey       String   @db.Text
  isAuthenticated Boolean @default(false)
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt
}

model Chat {
  id               Int       @id @default(autoincrement())
  chatId           BigInt    @unique
  title            String?   @db.VarChar(256)
  type             ChatType
  participantsCount Int?
  accessHash       String?   @db.VarChar(64)
  isForum          Boolean   @default(false)
  owner            User      @relation(fields: [ownerId], references: [id])
  ownerId          Int
  topics           Topic[]
  messages         Message[]
  createdAt        DateTime  @default(now())
}

model Topic {
  id        Int      @id @default(autoincrement())
  topicId   BigInt
  name      String   @db.VarChar(256)
  chat      Chat     @relation(fields: [chatId], references: [id])
  chatId    Int
  messages  Message[]
  @@unique([topicId, chatId])
}

model Message {
  id        Int       @id @default(autoincrement())
  messageId BigInt
  date      DateTime
  chat      Chat      @relation(fields: [chatId], references: [id])
  chatId    Int
  topic     Topic?    @relation(fields: [topicId], references: [id])
  topicId   Int?
  media     Media?
  downloadLogs DownloadLog[]
  @@unique([messageId, chatId])
}

model Media {
  id          Int       @id @default(autoincrement())
  type        MediaType
  filePath    String    @db.Text
  fileSize    Int?
  message     Message   @relation(fields: [messageId], references: [id])
  messageId   Int
  createdAt   DateTime  @default(now())
}

model DownloadLog {
  id          Int           @id @default(autoincrement())
  timestamp   DateTime      @default(now())
  filename    String        @db.Text
  status      DownloadStatus
  errorMsg    String?       @db.Text
  message     Message       @relation(fields: [messageId], references: [id])
  messageId   Int
  mediaType   MediaType
  topicName   String?       @db.VarChar(256)
}