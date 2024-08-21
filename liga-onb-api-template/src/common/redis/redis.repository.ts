import { Injectable } from '@nestjs/common';
import { RedisService } from 'nestjs-redis';

@Injectable()
export class RedisRepository {
  constructor(private readonly redisService: RedisService) {}

  private getClient() {
    return this.redisService.getClient();
  }

  public async getMultipleValues(keys: string[]): Promise<string[]> {
    if (!keys.length) return [];
    const client = this.getClient();
    return client.mget(...keys);
  }

  public async getRangeFromSortedSet(key: string, offset = 0, limit = 100): Promise<string[]> {
    const client = this.getClient();
    return client.zrange(key, offset, limit);
  }

  public async getKeysByPattern(pattern: string): Promise<string[]> {
    const client = this.getClient();
    return client.keys(`*${pattern}*`);
  }

  public async getDatabaseSize(): Promise<number> {
    const client = this.getClient();
    return client.dbsize();
  }
}
