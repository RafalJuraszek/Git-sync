import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {IpcRenderer} from 'electron';

@Component({
  selector: 'app-add-repo',
  templateUrl: './add-repo.component.html',
  styleUrls: ['./add-repo.component.css']
})
export class AddRepoComponent implements OnInit {

  repoForm: FormGroup;
  private ipc: IpcRenderer;
  selectedDir;

  constructor() {
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
      url: new FormControl(null),
      password: new FormControl(null),
      login: new FormControl(null)
    });

    this.ipc.on('selected-dir', (event, arg) => {
      console.log(arg)
      this.selectedDir = arg.toString();
    });
  }

  pickPath() {
    this.ipc.send('open-file-dialog-for-dir');

  }

}
