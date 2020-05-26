import {Component, OnInit, ViewChild} from '@angular/core';
import {Router} from '@angular/router';
import {IpcRenderer} from 'electron';
import {RepoService} from '../services/repo.service';
import {RepoModel} from '../model/repo.model';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  providers: [RepoService]
})
export class HomeComponent implements OnInit {

  repos: RepoModel[] = [];

  constructor(private router: Router, private repoService: RepoService) {

  }

  ngOnInit() {
    this.repoService.getRepos().subscribe(repos => {
      console.log(repos)
      this.repos = repos;
    });
    //to tylko symuluje ze cos dostalismy, bo nie mam backendu
    //this.repos.push(new RepoModel('1', 'url', 'rafal', 'elo', 'c', null));
  }

  checkRepo(repo) {
    this.router.navigateByUrl('/addRepo', {state: {repo: repo}});
  }

  add() {
    this.router.navigateByUrl('/addRepo');
  }

  delete(repo) {
    this.repoService.deleteRepo(repo).subscribe(response => {

      const repoToDelete = this.repos.indexOf(repo);
      this.repos.splice(repoToDelete, 1);
    });
  }


}
