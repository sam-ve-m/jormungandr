import { Injectable } from '@nestjs/common';
import { Model } from 'mongoose';
import { BaseRepository } from '../../common/database/database.repository';
import { InjectModel } from '@nestjs/mongoose';
import { User } from './user.model';

@Injectable()
export class UserRepository extends BaseRepository<User> {
  constructor(@InjectModel('User') userModel: Model<User>) {
    super(userModel);
  }
}
