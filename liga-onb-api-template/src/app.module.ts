import { HttpModule } from '@nestjs/axios';
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { TerminusModule } from '@nestjs/terminus';
import { envValidate } from './common/config/env.validation';
import { HealthController } from './modules/health/health.controller';
import { DatabaseModule } from './common/database/database.module';
import { UsersModule } from './modules/user/user.module';

@Module({
  controllers: [HealthController],
  imports: [
    HttpModule,
    ConfigModule.forRoot({
      isGlobal: true,
      validate: envValidate,
    }),
    TerminusModule,
    UsersModule,
    DatabaseModule,
  ],
})
export class AppModule {}
