import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {RepoModel} from '../model/repo.model';
import {tap} from 'rxjs/operators';


@Injectable()
export class RepoService {

  basicApiUrl: string = 'http://localhost:4200/api/';
  repos: RepoModel[] = [];

  constructor(private http: HttpClient) {
  }

  getRepos(): Observable<RepoModel[]> {

    return this.http.get<RepoModel[]>(this.basicApiUrl + 'repos').pipe(tap(repos => {

      this.repos = repos;
    }));
  }


  postRepo(repo) {

    this.http.post(this.basicApiUrl + 'addRepo', repo).subscribe(data => {
      this.repos.push(repo);
    });
  }


  deleteRepo(repo): Observable<any> {
    return this.http.delete(this.basicApiUrl + 'repos/' + repo.id);
  }



}

