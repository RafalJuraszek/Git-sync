import {Component} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  basicApiUrl = 'http://localhost:4200/synchronizer';
  title = 'management-panel';
  helloMessage;

  constructor(private http: HttpClient) {
  }


  synchronize() {
  this.http.get<any>(this.basicApiUrl).subscribe((data) => this.helloMessage = data);
}
}
