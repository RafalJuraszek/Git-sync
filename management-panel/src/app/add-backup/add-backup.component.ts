import { Component, ElementRef, ViewChild, OnInit } from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {Router} from '@angular/router';
import {RepoModel} from "../model/repo.model";
import {RepoService} from "../services/repo.service";
import {BackupModel} from "../model/backup.model";

@Component({
  selector: 'app-add-backup',
  templateUrl: './add-backup.component.html',
  styleUrls: ['./add-backup.component.css'],
  providers: [RepoService]
})
export class AddBackupComponent implements OnInit {

  @ViewChild('url', {static: false}) url: ElementRef;
  @ViewChild('login', {static: false}) login: ElementRef;
  @ViewChild('password', {static: false}) password: ElementRef;
  @ViewChild('frequency', {static: false}) frequency: ElementRef;

  backupForm: FormGroup;
  currentRepo: RepoModel;
  allBackups: BackupModel[] = [];
  newBackups: BackupModel[] = [];

  constructor(private router: Router, private repoService: RepoService) {
    this.currentRepo = this.router.getCurrentNavigation().extras.state?.repo;
    this.allBackups = this.currentRepo.backups;
  }

  ngOnInit() {
    this.backupForm = new FormGroup({
      url: new FormControl(null),
      login: new FormControl(null),
      password: new FormControl(null)
    });
  }

  addBackup() {
    if (this.allBackups.map(backup => backup.url).includes(this.url.nativeElement.value)) {
      window.alert("Backup with given url already exist!");
      return;
    }

    const {url, login, password} = this.backupForm.value;
    const newBackup = new BackupModel(url, login, password);
    this.allBackups.push(newBackup);
    this.newBackups.push(newBackup);
    this.clearForm();
  }

  onSubmit() {
    const newFrequency = parseInt(this.frequency.nativeElement.value);
    this.repoService.modifyRepo(this.currentRepo.id, this.newBackups, newFrequency);
    this.router.navigateByUrl('/');
  }

  private clearForm() {
    this.url.nativeElement.value = "";
    this.login.nativeElement.value = "";
    this.password.nativeElement.value = "";
  }
}
