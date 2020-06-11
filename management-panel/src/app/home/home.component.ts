import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {RepoService} from '../services/repo.service';
import {RepoModel} from '../model/repo.model';
import {BackupModel} from "../model/backup.model";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  providers: [RepoService]
})
export class HomeComponent implements OnInit {
  repos: RepoModel[] = [];
  running = true;
  dialog;

  constructor(private router: Router, private repoService: RepoService) {

    if ((<any> window).require) {
      try {
        const Dialogs = (<any> window).require('dialogs')
        this.dialog = Dialogs();
      } catch (e) {
        throw e;
      }
    } else {
      console.warn('App not running inside Electron!');
    }
  }

  ngOnInit() {
    this.repoService.getRepos().subscribe((repos) => {
      console.log(repos);
      this.repos = repos;
      this.running = false;
    }, (error) => {
      console.log(error);
      if (error.status === 504) {
        this.dialog.alert('Problem with connecting to the synchronizer');
      } else {
        this.dialog.alert(error.error.message);
      }
      this.running = false;
    });

    // to refactor during integration with backend
    const backupsArray1: BackupModel[] = [];
    const backupsArray2: BackupModel[] = [new BackupModel("url123", "logininin", "haselko")];


    console.log(this.repos);
  }

  checkRepo(repo) {
    this.router.navigateByUrl('/addBackup', {state: {repo}});
  }

  add() {
    this.router.navigateByUrl('/addRepo');
  }

  delete(repo) {
    this.repoService.deleteRepo(repo).subscribe((response) => {
      const repoToDelete = this.repos.indexOf(repo);
      this.repos.splice(repoToDelete, 1);
    });
  }
}
