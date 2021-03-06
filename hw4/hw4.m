clear all
clc
close all

k1=4;
E1=csvread('example1.dat');
algorithm(E1, k1);

%k2=2;
%E2=csvread('example2.dat');
%algorithm(E2, k2);


function [clusters, L]=algorithm(E, k)
    % step 1
    % we can just simply use the adjacency matrix to compute the affinity
    % matrix since there is no disteance on edges, which is always 1
    col1=E(:,1);
    col2=E(:,2);
    max_ids = max(max(col1,col2));
    As= sparse(col1, col2, 1, max_ids, max_ids);
    A= full(adjacency(graph(As)));
    figure(1);
    spy(A);
    figure(2);
    plot(graph(A),'Layout','force');
    figure(3);
    h=plot(graph(A),'Layout','force');
       
    % step 2
    D=diag(sum(A,2));
    L=(D^(-1/2)*A*D^(-1/2));
    
    
    % step 3
    [V,d]=eigs(L,k);
      
    %step 4
    Y=V./sum(V.*V,2).^(1/2);
    
    %step 5
    clusters = kmeans(Y,k);
    % clusters = [idx,c];
    
    %step 6
    cluster_colors=hsv(k);
    for i=1:k
        cluster_members=find(clusters==i);
        highlight(h, cluster_members , 'NodeColor', cluster_colors(i,:))
    end
    figure(4)
    Lap = D - A;
    [F_V,~] = eigs(Lap,2,'SA');
    plot(sort(F_V(:,2)),'-*')
    figure(5)
    [F_V,~] = eigs(L,2,'SA');
    plot(sort(F_V(:,2)),'-*')

    % Visualization of the Sorted Fiedler Vector
end

