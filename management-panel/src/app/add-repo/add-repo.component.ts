import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {IpcRenderer} from 'electron';
import {BackupModel} from '../model/backup.model';
import {RepoModel} from '../model/repo.model';
import {RepoService} from '../services/repo.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-add-repo',
  templateUrl: './add-repo.component.html',
  styleUrls: ['./add-repo.component.css'],
  providers: [RepoService]
})
export class AddRepoComponent implements OnInit {

  @ViewChild('url', {static: false}) url: ElementRef;
  @ViewChild('login', {static: false}) login: ElementRef;
  @ViewChild('password', {static: false}) password: ElementRef;

  repoForm: FormGroup;
  private ipc: IpcRenderer;
  selectedDir = '';
  backups: BackupModel[] = [];

  constructor(private router: Router, private repoService: RepoService) {
    console.log(this.router.getCurrentNavigation().extras.state)
    if ((<any> window).require) {
      try {
        this.ipc = (<any> window).require('electron').ipcRenderer;


      } catch (e) {
        throw e;
      }
    } else {
      console.warn('App not running inside Electron!');
    }
  }

  ngOnInit(): void {
    this.repoForm = new FormGroup({
      id: new FormControl(null),
      url: new FormControl(null),
      password: new FormControl(null),
      login: new FormControl(null),
      path: new FormControl(null)
    });

    this.ipc.on('selected-dir', (event, arg) => {
      console.log(arg);
      this.selectedDir = arg.toString();
    });
  }

  pickPath() {
    this.ipc.send('open-file-dialog-for-dir');

  }

  submit(){

    const id = this.repoForm.value.id;
    const url = this.repoForm.value.url;
    const login = this.repoForm.value.login;
    const password = this.repoForm.value.password;
    const path = this.repoForm.value.path;

    const resultRepo = new RepoModel(id, url, login, password, path, this.backups);

    this.repoService.postRepo(resultRepo);
    this.router.navigateByUrl('/');

  }

  addBackup() {
    const backupUrl = this.url.nativeElement.value;
    const backupLogin = this.login.nativeElement.value;
    const backupPassword = this.password.nativeElement.value;
    const newBackup = new BackupModel(backupUrl, backupLogin, backupPassword);
    this.backups.push(newBackup);
  }


}
