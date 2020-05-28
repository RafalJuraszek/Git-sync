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

  constructor(private router: Router, private repoService: RepoService) {
  }

  ngOnInit() {
    this.repoService.getRepos().subscribe((repos) => {
      console.log(repos);
      this.repos = repos;
    });

    // to refactor during integration with backend
    const backupsArray1: BackupModel[] = [];
    const backupsArray2: BackupModel[] = [new BackupModel("url123", "logininin", "haselko")];

    const mockRepo1 = new RepoModel(
      'RakoczyRepo',
      'anyUrl1',
      'rakoczy',
      'password123',
      '/path/to/rakoczy/repo',
      backupsArray1
    );
    const mockRepo2 = new RepoModel(
      'MyRepo',
      'anyUrl2',
      'me',
      'me123',
      '/path/to/my/repo',
      backupsArray2
    );
    this.repos.push(mockRepo1, mockRepo2);
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
