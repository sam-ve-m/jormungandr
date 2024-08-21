import { Module } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { RedisModule as RedisModuleNest } from 'nestjs-redis';

@Module({
  imports: [
    RedisModuleNest.forRootAsync({
      useFactory: async (configService: ConfigService) => {
        return {
          url: configService.get(`REDIS_CONFIG`),
        };
      },
      inject: [ConfigService],
    }),
  ],
  providers: [],
})
export class RedisModule {}
