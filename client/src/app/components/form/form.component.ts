import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

const API_URL: string = 'http://localhost:5000';

interface AnalysisResult {
  avg_word: number,
  sentiment: string,
  word_count: string
}

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss']
})
export class FormComponent implements OnInit {

  public result: AnalysisResult;

  public form = new FormGroup({
    text: new FormControl()
  });

  constructor(private http: HttpClient) { }

  ngOnInit() {
  }

  public onSubmit(): void {
    const text = this.form.get('text').value;
    this.result = null;
    this.http.post<any>(`${API_URL}/analize`, { text }).subscribe(res => this.result = res.result);
  }
}
