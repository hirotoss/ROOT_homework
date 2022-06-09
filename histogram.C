#include "TH1D.h"
#include "TCanvas.h"
#include <bits/stdc++.h>
using namespace std;

void fill_from_file(TH1D* hist, TString filename){
    ifstream ifs(filename);
    double val;
    while(ifs >> val){
        hist->Fill(val);
    }
}

void histogram(){
    //make canvas
    TCanvas* c1 = new TCanvas();

    //bin setting
    int total_bin = 50;
    double min_bin = 0;
    double max_bin = 10;

    //make histogram
    TH1D* hist = new TH1D("hist", "", total_bin, min_bin, max_bin);

    //fill histogram
    fill_from_file(hist, "hist_data.txt");

    //modify histogram
    hist->SetTitle(";Access time(sec);Counts/0.2sec");
    hist->SetFillColor(4);

    //draw histogram
    hist->Draw();

    //save figure
    c1->Print("figure.svg");
    c1->Print("figure.pdf");
}