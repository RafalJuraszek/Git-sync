import {Component, OnInit, ViewChild} from '@angular/core';
import {Router} from '@angular/router';
import {IpcRenderer} from 'electron';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  private ipc: IpcRenderer;
  selectedDir;

  constructor(private router: Router) {
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

  ngOnInit() {
    this.ipc.on('selected-dir', (event, arg) => {
      console.log(arg)
      this.selectedDir = arg.toString();
    });
  }

  pickPath() {
    this.ipc.send('open-file-dialog-for-dir');

  }
  save() {
    console.log(this.selectedDir)
  }

}
