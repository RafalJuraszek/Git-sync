import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {IpcRenderer} from 'electron';
import {RepoService} from '../services/repo.service';
import {RepoModel} from '../model/repo.model';


@Component({
  selector: 'app-notify',
  templateUrl: './notify.component.html',
  styleUrls: ['./notify.component.css'],
  providers: [RepoService]
})
export class NotifyComponent implements OnInit {
  repos: RepoModel[] = [];
  selectedValue;
  isNotificationSentSuccessfully: boolean = false;
  isError: boolean = false;
  private ipc: IpcRenderer;

  constructor(private router: Router, private repoService: RepoService) {
    if ((<any>window).require) {
      try {
        this.ipc = (<any>window).require('electron').ipcRenderer;
      } catch (e) {
        throw e;
      }
    } else {
      console.warn('App not running inside Electron!');
    }
  }

  ngOnInit(): void {
    this.repoService.getRepos().subscribe((repos) => (this.repos = repos));

  }

  notify() {
    console.log(this.selectedValue)
    if (this.selectedValue === undefined) return;
    this.resetFlags();

    // should work after integration with backend
    this.repoService.notify(this.selectedValue).subscribe((data: Response) => {
      this.isNotificationSentSuccessfully = true;
      const repoWithSentNotification: RepoModel = this.repos.find(repo => repo.id === this.selectedValue);
      const index: number = this.repos.indexOf(repoWithSentNotification);
      this.repos.splice(index, 1);
    }, (err) =>{
      this.isError = true;
    });
  }

  private resetFlags() {
    this.isNotificationSentSuccessfully = false;
    this.isError = false;
  }
}
