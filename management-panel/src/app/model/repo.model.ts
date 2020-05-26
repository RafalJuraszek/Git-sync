import {BackupModel} from './backup.model';

export class RepoModel {

  constructor(public id: string, public url: string, public login: string
              , public password: string, public path: string, public backups: BackupModel[]) {
  }
}
