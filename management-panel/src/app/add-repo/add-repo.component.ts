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
    // to refactor during integration with backend
    const mockRepo1 = new RepoModel(
      'RakoczyRepo',
      'anyUrl1',
      'rakoczy',
      'password123',
      '/path/to/rakoczy/repo',
      [],
      2
    );
    const mockRepo2 = new RepoModel('MyRepo',
      'anyUrl2',
      'me',
      'me123',
      '/path/to/my/repo',
      [],
      2
    );
    this.repoService.repos.push(mockRepo1, mockRepo2);

    this.repoForm = new FormGroup({
      id: new FormControl(null),
      url: new FormControl(null),
      password: new FormControl(null),
      login: new FormControl(null),
      path: new FormControl(null),
      frequency: new FormControl(null)
    });

    this.ipc.on('selected-dir', (event, arg) => {
      console.log(arg);
      this.selectedDir = arg.toString();
    });
  }

  pickPath() {
    this.ipc.send('open-file-dialog-for-dir');
  }

  submit() {
    const {id, url, login, password, path, frequency} = this.repoForm.value;
    if (this.repoService.repos.map(repo => repo.id).includes(id)) {
      window.alert("Repository with given ID already exist!");
      return;
    }

    const resultRepo = new RepoModel(id, url, login, password, path, this.backups, frequency);
    this.repoService.postRepo(resultRepo);
    this.router.navigateByUrl('/');
  }

  addBackup() {
    if (this.backups.map(backup => backup.url).includes(this.url.nativeElement.value)) {
      window.alert("Backup with given url already exist!");
      return;
    }

    const backupUrl = this.url.nativeElement.value;
    const backupLogin = this.login.nativeElement.value;
    const backupPassword = this.password.nativeElement.value;
    const newBackup = new BackupModel(backupUrl, backupLogin, backupPassword);
    this.backups.push(newBackup);
    this.clearBackup()
  }

  private clearBackup() {
    this.url.nativeElement.value = "";
    this.login.nativeElement.value = "";
    this.password.nativeElement.value = "";
  }
}
