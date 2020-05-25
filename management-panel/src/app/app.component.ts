import {Component, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {MenuItem} from 'primeng';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  basicApiUrl = 'http://localhost:4200/synchronizer';
  title = 'management-panel';
  helloMessage;

  items: MenuItem[];

  ngOnInit() {
    this.items = [{
      label: 'File',
      items: [
        {label: 'New', icon: 'pi pi-plus', url: 'http://www.primefaces.org/primeng'},
        {label: 'Open', icon: 'pi pi-download', routerLink: ['/pagename']},
        {label: 'Recent Files', icon: 'pi pi-download', routerLink: ['/pagename'], queryParams: {'recent': 'true'}}
      ]
    }]
  }

  constructor(private http: HttpClient) {
  }


  synchronize() {
  this.http.get<any>(this.basicApiUrl).subscribe((data) => this.helloMessage = data);
}
}
