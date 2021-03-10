create table condo (
    condo_base_bbl      number(10,0)
   ,condo_billing_bbl   number(10,0)
   ,primary key (condo_base_bbl, condo_billing_bbl)
);
create table condo_load (
    condo_base_bbl      number(10,0)
   ,condo_billing_bbl   number(10,0)
); 
create table pluto_load (
    bbl                 number(10,0)
); 
