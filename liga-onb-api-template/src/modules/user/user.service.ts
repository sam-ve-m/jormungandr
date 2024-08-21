import { Injectable } from '@nestjs/common';
import { User } from './user.model';
import { UserRepository } from './user.repository';

@Injectable()
export class UserService {
  constructor(private readonly userRepository: UserRepository) {}

  async findAll(): Promise<User[]> {
    return this.userRepository.findAll();
  }

  async findById(id: string): Promise<User> {
    return this.userRepository.findById(id);
  }

  async create(user: User): Promise<User> {
    return this.userRepository.create(user);
  }

  async update(id: string, user: User): Promise<User> {
    return this.userRepository.update(id, user);
  }

  async delete(id: string): Promise<User> {
    return this.userRepository.delete(id);
  }
}
