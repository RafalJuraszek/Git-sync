import {ChangeDetectorRef, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
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
  validPath = true;
  running = false;

  constructor(private router: Router, private repoService: RepoService, private changer: ChangeDetectorRef) {
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
      path: new FormControl(null),
      frequency: new FormControl(null)
    });

    this.ipc.on('selected-dir', (event, arg) => {
      console.log(arg);
      if (arg === 'not-empty') {
        this.validPath = false;
      } else {
        this.validPath = true;
        this.selectedDir = arg.toString();
      }
      this.running = false;
      this.changer.detectChanges();
    });
    this.ipc.on('error', (event, arg) => {
      this.running = false;
      this.changer.detectChanges();
    });
  }

  pickPath() {
    this.running = true;
    this.ipc.send('open-file-dialog-for-dir');
  }

  submit() {
    const {id, url, login, password, path, frequency} = this.repoForm.value;
    if (this.repoService.repos.map(repo => repo.id).includes(id)) {
      window.alert('Repository with given ID already exist!');
      return;
    }

    const resultRepo = new RepoModel(id, url, login, password, path, this.backups, frequency);
    this.repoService.postRepo(resultRepo).subscribe(data => {
      this.router.navigateByUrl('/');
    }, (error) => {
      console.log(error);
      if (error.status === 504) {
        window.alert('Problem with connecting to the synchronizer');
      } else {
        window.alert(error.error);
      }
    });

  }

  addBackup() {
    if (this.backups.map(backup => backup.url).includes(this.url.nativeElement.value)) {
      window.alert('Backup with given url already exist!');
      return;
    }

    const backupUrl = this.url.nativeElement.value;
    const backupLogin = this.login.nativeElement.value;
    const backupPassword = this.password.nativeElement.value;
    const newBackup = new BackupModel(backupUrl, backupLogin, backupPassword);
    this.backups.push(newBackup);
    this.clearBackup();
  }

  private clearBackup() {
    this.url.nativeElement.value = '';
    this.login.nativeElement.value = '';
    this.password.nativeElement.value = '';
  }
}
