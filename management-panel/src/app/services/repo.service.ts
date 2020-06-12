import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {RepoModel} from '../model/repo.model';
import {tap} from 'rxjs/operators';
import {BackupModel} from "../model/backup.model";


@Injectable()
export class RepoService {

  basicApiUrl: string = 'http://localhost:5000/api/'; //'http://localhost:4200/api/';
  repos: RepoModel[] = [];

  constructor(private http: HttpClient) {
  }

  getRepos(): Observable<RepoModel[]> {

    return this.http.get<RepoModel[]>(this.basicApiUrl + 'repos').pipe(tap(repos => {
      console.log(repos)
      this.repos = repos;
    }));
  }

  postRepo(repo): Observable<any> {

    return this.http.post(this.basicApiUrl + 'addRepo', repo).pipe(tap(data => {
      this.repos.push(repo);
    }));
  }

  deleteRepo(repo): Observable<any> {
    return this.http.delete(this.basicApiUrl + 'repos/' + repo.id);
  }

  notify(id: string): Observable<any> {
    return this.http.post(`${this.basicApiUrl}notify`, {id});
  }

  modifyRepo(repoId: string, backups: BackupModel[], frequency: number): Observable<any> {
    const options = {headers: new HttpHeaders({'Content-Type':  'application/json'})};
    const body = {
      id: repoId,
      backups,
      frequency
    };
    return this.http.put(`${this.basicApiUrl}modifyRepo`, body, options);
  }

  deleteBackup(repoId: string, backupUrl: string): Observable<any> {
    const options = {
      headers: new HttpHeaders({'Content-Type': 'application/json'}),
      body: {url: backupUrl},
    };
    return this.http.delete(`${this.basicApiUrl}repos/${repoId}`, options);
  }
}

