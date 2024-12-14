touch ~/.bashrc
echo '. ~/.bashrc' >> ~/.profile
wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
bash ./Mambaforge-Linux-x86_64.sh -b
/home/azureuser/mambaforge/bin/mamba init
/home/azureuser/mambaforge/bin/mamba install -y zsh
git config --global credential.helper "cache --timeout=604800"
touch ~/.zshrc
echo '
case $- in
    *i*) exec zsh -l
esac' >> ~/.bashrc
ZSH="${ZSH:-$HOME/.oh-my-zsh}"
REPO=${REPO:-ohmyzsh/ohmyzsh}
REMOTE=${REMOTE:-https://github.com/${REPO}.git}
BRANCH=${BRANCH:-master}
git init --quiet "$ZSH" && cd "$ZSH" \
&& git config core.eol lf \
&& git config core.autocrlf false \
&& git config fsck.zeroPaddedFilemode ignore \
&& git config fetch.fsck.zeroPaddedFilemode ignore \
&& git config receive.fsck.zeroPaddedFilemode ignore \
&& git config oh-my-zsh.remote origin \
&& git config oh-my-zsh.branch "$BRANCH" \
&& git remote add origin "$REMOTE" \
&& git fetch --depth=1 origin \
&& git checkout -b "$BRANCH" "origin/$BRANCH" && cd -
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
sed -i 's/ZSH_THEME=\"robbyrussell\"/ZSH_THEME=\"powerlevel10k\/powerlevel10k\"/g' ~/.zshrc
wget -O ~/.p10k.zsh  https://gist.github.com/AgrawalAmey/8bd8474d0cffda80aa4fdaab3b0478e1/raw/20e72101c8a5ea84be24fca7df54d59ddd77cd44/.p10k.zsh 
wget -O ~/.zshrc  https://gist.githubusercontent.com/AgrawalAmey/8bd8474d0cffda80aa4fdaab3b0478e1/raw/20e72101c8a5ea84be24fca7df54d59ddd77cd44/.zshrc
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
source ~/mambaforge/bin/activate
~/.fzf/install --all
/home/azureuser/mambaforge/bin/mamba init zsh
